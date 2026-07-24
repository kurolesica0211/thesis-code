================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Princess Isabelle Françoise Hélène Marie d'Orléans (27 November 1900, Le Nouvion-en-Thiérache, France – 12 February 1983, Neuilly-sur-Seine, France) was a member of the House of Orléans and, by marriage, a member of the ducal Harcourt family and of the princely House of Murat.
She was one of the four children of Prince Jean, Duke of Guise (1874–1940), who would become the Orleanist pretender to the French throne in 1926, and Princess Isabelle of Orléans.
Marriages

In 1923 the tradition of Orléans princesses marrying only other royalty (since the alleged 1681 wedding of La Grande Mademoiselle) was dispensed with, as nearly all of her relatives attended Isabelle's wedding at Amélie of Orléans château in Le Chesnay on 12 September to Count Bruno d'Harcourt (1899–1930), son of Count Eugène d'Harcourt and Armande de Pierre de Bernis.
An automobile racer, Harcourt was killed during practice for the Moroccan Grand Prix, leaving his wife with four children:


As a widow, Isabelle remarried the Bonapartist Prince Pierre Murat (1900–1948) in 1934, at Jouy-en-Josas, "upon renunciation of the rank and prerogatives appertaining to princesses of the House of France".
Prince Murat was a  great-grandson of Prince Lucien Murat.
In 1940, as World War II began and when her father died, Isabelle again took refuge at the family estate, Larache, in Morocco, where she shared quarters with her mother, and her elder sister the widowed Princess Françoise of Greece, along with her brother Henri, Count of Paris and the latter's son, Prince Michel d'Orléans.Isabella often visited her parents in Morocco, Belgium and France, especially during World 
War II.
In 1953, her younger sister,Princess Françoise, widow of Prince Christopher of Greece, died in her Paris home after a long period of depression.
Princess Isabella herself died in 1983 and is buried in the Montparnasse Cemetery in Paris.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns1:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns2:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns2:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (5e379d56-6d9b-4ee8-9d1b-e44e6d536fb9)
 Call ID: 5e379d56-6d9b-4ee8-9d1b-e44e6d536fb9
  Args:
    type: :Person
    source: Isabelle_dOrleans
  AssignClass (171bebe7-1efb-4228-bcf9-19afd6c0d6e7)
 Call ID: 171bebe7-1efb-4228-bcf9-19afd6c0d6e7
  Args:
    type: :Woman
    source: Isabelle_dOrleans
  AddLiteral (3d11159c-73db-4eb5-8382-80b9e2110a9b)
 Call ID: 3d11159c-73db-4eb5-8382-80b9e2110a9b
  Args:
    relation: :hasBirthYear
    literal_value: 1900
    source: Isabelle_dOrleans
    literal_type: xsd:integer
  AddLiteral (8e33c004-cc3d-43c1-b79c-a2b5b702179c)
 Call ID: 8e33c004-cc3d-43c1-b79c-a2b5b702179c
  Args:
    literal_type: xsd:integer
    literal_value: 1983
    source: Isabelle_dOrleans
    relation: :hasDeathYear
  AssignClass (f9ff01a3-a36e-4872-b8e8-a7fb81482db0)
 Call ID: f9ff01a3-a36e-4872-b8e8-a7fb81482db0
  Args:
    type: :Person
    source: Prince_Jean_Duke_of_Guise
  AssignClass (acb88e42-f109-48a8-b93b-23e843c81876)
 Call ID: acb88e42-f109-48a8-b93b-23e843c81876
  Args:
    type: :Man
    source: Prince_Jean_Duke_of_Guise
  AddLiteral (82733571-4c99-4259-a877-f256d7e309dc)
 Call ID: 82733571-4c99-4259-a877-f256d7e309dc
  Args:
    relation: :hasBirthYear
    literal_value: 1874
    source: Prince_Jean_Duke_of_Guise
    literal_type: xsd:integer
  AddLiteral (1ca58eb7-ee97-44a7-a339-ab2fec6cc3d4)
 Call ID: 1ca58eb7-ee97-44a7-a339-ab2fec6cc3d4
  Args:
    literal_type: xsd:integer
    literal_value: 1940
    source: Prince_Jean_Duke_of_Guise
    relation: :hasDeathYear
  AssignClass (2335994b-d640-4786-8591-f6dca7156d53)
 Call ID: 2335994b-d640-4786-8591-f6dca7156d53
  Args:
    type: :Person
    source: Princess_Isabelle_of_Orleans_Mother
  AssignClass (54ad0c1d-d9d9-479b-a4ab-5243a3bdc535)
 Call ID: 54ad0c1d-d9d9-479b-a4ab-5243a3bdc535
  Args:
    type: :Woman
    source: Princess_Isabelle_of_Orleans_Mother
  AddTriple (ecf9de19-3002-4ef9-92b1-237510fa8ef7)
 Call ID: ecf9de19-3002-4ef9-92b1-237510fa8ef7
  Args:
    target: Isabelle_dOrleans
    source: Prince_Jean_Duke_of_Guise
    relation: :isFatherOf
  AddTriple (8caf6d7e-b165-4c01-b79a-dd05780759ad)
 Call ID: 8caf6d7e-b165-4c01-b79a-dd05780759ad
  Args:
    target: Isabelle_dOrleans
    source: Princess_Isabelle_of_Orleans_Mother
    relation: :isMotherOf
  AssignClass (1f1a27b3-5e84-4a0e-bc59-9189dfcff9ba)
 Call ID: 1f1a27b3-5e84-4a0e-bc59-9189dfcff9ba
  Args:
    type: :Person
    source: Count_Bruno_dHarcourt
  AssignClass (da2c6c91-5bb8-4cac-bac0-3e45a0923a90)
 Call ID: da2c6c91-5bb8-4cac-bac0-3e45a0923a90
  Args:
    type: :Man
    source: Count_Bruno_dHarcourt
  AddLiteral (74a0702a-a704-4697-984b-c1057bc2050e)
 Call ID: 74a0702a-a704-4697-984b-c1057bc2050e
  Args:
    relation: :hasBirthYear
    source: Count_Bruno_dHarcourt
    literal_value: 1899
    literal_type: xsd:integer
  AddLiteral (0199fbd6-82ac-4936-a3b7-5be30640e137)
 Call ID: 0199fbd6-82ac-4936-a3b7-5be30640e137
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Count_Bruno_dHarcourt
    literal_value: 1930
  AddLiteral (fb9df8b6-4351-42c2-bf52-002efe60379f)
 Call ID: fb9df8b6-4351-42c2-bf52-002efe60379f
  Args:
    relation: :hasMarriageYear
    source: Isabelle_dOrleans
    literal_value: 1923
    literal_type: xsd:integer
  AddTriple (7d3f356b-640c-422c-9296-620887ccf50d)
 Call ID: 7d3f356b-640c-422c-9296-620887ccf50d
  Args:
    relation: :hasRelation
    target: Count_Bruno_dHarcourt
    source: Isabelle_dOrleans
  AssignClass (a884f06f-8afd-4cc1-bc4c-46cbe50dc02b)
 Call ID: a884f06f-8afd-4cc1-bc4c-46cbe50dc02b
  Args:
    type: :Person
    source: Prince_Pierre_Murat
  AssignClass (231f5a36-ff4c-43ea-9e46-fa394b211d16)
 Call ID: 231f5a36-ff4c-43ea-9e46-fa394b211d16
  Args:
    type: :Man
    source: Prince_Pierre_Murat
  AddLiteral (100c3e94-6bef-46d6-ad0b-007b34d48cf4)
 Call ID: 100c3e94-6bef-46d6-ad0b-007b34d48cf4
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Prince_Pierre_Murat
    literal_value: 1900
  AddLiteral (e3d069f0-98c3-43d3-b561-2bbcd9b8df79)
 Call ID: e3d069f0-98c3-43d3-b561-2bbcd9b8df79
  Args:
    literal_type: xsd:integer
    literal_value: 1948
    source: Prince_Pierre_Murat
    relation: :hasDeathYear
  AddLiteral (3026ec69-8471-49ef-9d78-a0d54520c6db)
 Call ID: 3026ec69-8471-49ef-9d78-a0d54520c6db
  Args:
    source: Isabelle_dOrleans
    literal_value: 1934
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (9ebfcb81-cd15-47d5-84d5-d94b01176cd4)
 Call ID: 9ebfcb81-cd15-47d5-84d5-d94b01176cd4
  Args:
    target: Prince_Pierre_Murat
    source: Isabelle_dOrleans
    relation: :hasRelation
  AssignClass (838f7ad7-42ba-4ce1-84a5-97d4e87a8ad5)
 Call ID: 838f7ad7-42ba-4ce1-84a5-97d4e87a8ad5
  Args:
    type: :Person
    source: Princess_Francoise_of_Greece
  AssignClass (34112662-b31e-423a-accf-bd1db5346032)
 Call ID: 34112662-b31e-423a-accf-bd1db5346032
  Args:
    type: :Woman
    source: Princess_Francoise_of_Greece
  AddTriple (744a8a8e-d4e8-4bb8-955c-c5a7b631c891)
 Call ID: 744a8a8e-d4e8-4bb8-955c-c5a7b631c891
  Args:
    relation: :isSisterOf
    target: Isabelle_dOrleans
    source: Princess_Francoise_of_Greece
  AssignClass (6b95fd80-aa73-4609-bd43-ba406cc11892)
 Call ID: 6b95fd80-aa73-4609-bd43-ba406cc11892
  Args:
    type: :Person
    source: Henri_Count_of_Paris
  AssignClass (4ebfd8c7-0e4a-400f-bf17-5f0c612d3665)
 Call ID: 4ebfd8c7-0e4a-400f-bf17-5f0c612d3665
  Args:
    type: :Man
    source: Henri_Count_of_Paris
  AddTriple (1acfd8a2-6f3e-4fc3-9b19-c6f91d580941)
 Call ID: 1acfd8a2-6f3e-4fc3-9b19-c6f91d580941
  Args:
    relation: :isBrotherOf
    source: Henri_Count_of_Paris
    target: Isabelle_dOrleans
  AssignClass (87bf7a3d-7f9a-46fa-ab7f-f5c26afd12ba)
 Call ID: 87bf7a3d-7f9a-46fa-ab7f-f5c26afd12ba
  Args:
    type: :Person
    source: Prince_Michel_dOrleans
  AssignClass (9e0a2ca4-f453-4820-9b77-cd7c4808a41b)
 Call ID: 9e0a2ca4-f453-4820-9b77-cd7c4808a41b
  Args:
    type: :Man
    source: Prince_Michel_dOrleans
  AddTriple (b6db4aea-446b-4b8b-bc21-ba23f01b086e)
 Call ID: b6db4aea-446b-4b8b-bc21-ba23f01b086e
  Args:
    relation: :isFatherOf
    target: Prince_Michel_dOrleans
    source: Henri_Count_of_Paris
  Finish (b842ce17-05b7-44ff-8a47-77856fe7aa75)
 Call ID: b842ce17-05b7-44ff-8a47-77856fe7aa75
  Args: