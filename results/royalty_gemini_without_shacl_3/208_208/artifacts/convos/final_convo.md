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
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns1:Variable .

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

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (8a679744-350a-414b-b3ec-6f04a6ac5805)
 Call ID: 8a679744-350a-414b-b3ec-6f04a6ac5805
  Args:
    type: :Woman
    source: Isabelle_dOrleans
  AssignClass (9a486e98-fc0a-4b55-b282-ef5a6be40dcc)
 Call ID: 9a486e98-fc0a-4b55-b282-ef5a6be40dcc
  Args:
    type: :Person
    source: Isabelle_dOrleans
  AddLiteral (701e5273-2b83-452c-b28f-b8745d70872c)
 Call ID: 701e5273-2b83-452c-b28f-b8745d70872c
  Args:
    literal_type: xsd:integer
    source: Isabelle_dOrleans
    literal_value: 1900
    relation: :hasBirthYear
  AddLiteral (890caefb-e5a1-4737-916d-0d46bd5ca03d)
 Call ID: 890caefb-e5a1-4737-916d-0d46bd5ca03d
  Args:
    literal_value: 1983
    relation: :hasDeathYear
    source: Isabelle_dOrleans
    literal_type: xsd:integer
  AssignClass (0cd87117-7fe1-4d57-9064-348773df48be)
 Call ID: 0cd87117-7fe1-4d57-9064-348773df48be
  Args:
    type: :Man
    source: Jean_Duke_of_Guise
  AssignClass (2b806c8d-c8e1-4cf4-9fe3-4c54ce710961)
 Call ID: 2b806c8d-c8e1-4cf4-9fe3-4c54ce710961
  Args:
    type: :Person
    source: Jean_Duke_of_Guise
  AddLiteral (6f4c1d44-3413-4455-af93-7f672ba0b68e)
 Call ID: 6f4c1d44-3413-4455-af93-7f672ba0b68e
  Args:
    relation: :hasBirthYear
    literal_value: 1874
    source: Jean_Duke_of_Guise
    literal_type: xsd:integer
  AddLiteral (fa06385e-f361-4abf-85f5-a7d9542e2a1a)
 Call ID: fa06385e-f361-4abf-85f5-a7d9542e2a1a
  Args:
    literal_value: 1940
    relation: :hasDeathYear
    source: Jean_Duke_of_Guise
    literal_type: xsd:integer
  AssignClass (d4957aa8-34df-429b-a976-d6cb1eb2417f)
 Call ID: d4957aa8-34df-429b-a976-d6cb1eb2417f
  Args:
    type: :Woman
    source: Isabelle_of_Orleans_Mother
  AssignClass (d00784bd-8b46-448c-8e9c-5e8a93b4c0bb)
 Call ID: d00784bd-8b46-448c-8e9c-5e8a93b4c0bb
  Args:
    type: :Person
    source: Isabelle_of_Orleans_Mother
  AddTriple (e2c74153-eb6d-41e2-a073-2641932caab6)
 Call ID: e2c74153-eb6d-41e2-a073-2641932caab6
  Args:
    target: Jean_Duke_of_Guise
    relation: :hasFather
    source: Isabelle_dOrleans
  AddTriple (24d8204b-fdae-46bc-a547-68a940823dac)
 Call ID: 24d8204b-fdae-46bc-a547-68a940823dac
  Args:
    source: Isabelle_dOrleans
    relation: :hasMother
    target: Isabelle_of_Orleans_Mother
  AssignClass (f0f76ea0-4b7b-47c3-8cce-537122f2d922)
 Call ID: f0f76ea0-4b7b-47c3-8cce-537122f2d922
  Args:
    type: :Man
    source: Bruno_dHarcourt
  AssignClass (1c59f633-34eb-4492-9348-ada605b17401)
 Call ID: 1c59f633-34eb-4492-9348-ada605b17401
  Args:
    type: :Person
    source: Bruno_dHarcourt
  AddLiteral (0622a700-4540-408d-860d-39a8d7dc75cf)
 Call ID: 0622a700-4540-408d-860d-39a8d7dc75cf
  Args:
    relation: :hasBirthYear
    literal_value: 1899
    source: Bruno_dHarcourt
    literal_type: xsd:integer
  AddLiteral (f6cba06a-3832-4383-a52e-542d361fdc66)
 Call ID: f6cba06a-3832-4383-a52e-542d361fdc66
  Args:
    relation: :hasDeathYear
    literal_value: 1930
    literal_type: xsd:integer
    source: Bruno_dHarcourt
  AddLiteral (07e33744-c0ee-4c6d-85c4-858645789689)
 Call ID: 07e33744-c0ee-4c6d-85c4-858645789689
  Args:
    relation: :hasMarriageYear
    literal_value: 1923
    source: Isabelle_dOrleans
    literal_type: xsd:integer
  AddTriple (3969a209-3fbf-4400-99ac-ca64026d4d6d)
 Call ID: 3969a209-3fbf-4400-99ac-ca64026d4d6d
  Args:
    target: Bruno_dHarcourt
    relation: :hasRelation
    source: Isabelle_dOrleans
  AssignClass (9aea0d11-9966-4749-a2c5-4fc2ae021245)
 Call ID: 9aea0d11-9966-4749-a2c5-4fc2ae021245
  Args:
    type: :Man
    source: Eugene_dHarcourt
  AssignClass (ce50811b-d511-4b89-aa96-98677da2c2c5)
 Call ID: ce50811b-d511-4b89-aa96-98677da2c2c5
  Args:
    type: :Person
    source: Eugene_dHarcourt
  AssignClass (711fe11a-b9cd-4de4-b9b8-429c7853bd4e)
 Call ID: 711fe11a-b9cd-4de4-b9b8-429c7853bd4e
  Args:
    type: :Woman
    source: Armande_de_Pierre_de_Bernis
  AssignClass (3d3b9599-88c4-40d3-9839-aee75f0e2784)
 Call ID: 3d3b9599-88c4-40d3-9839-aee75f0e2784
  Args:
    type: :Person
    source: Armande_de_Pierre_de_Bernis
  AddTriple (6cc9ce8a-b090-40fc-9b2a-867b8d7118c0)
 Call ID: 6cc9ce8a-b090-40fc-9b2a-867b8d7118c0
  Args:
    source: Bruno_dHarcourt
    relation: :hasFather
    target: Eugene_dHarcourt
  AddTriple (3be0039e-4ccd-46d6-a8fe-929e4f8e9afd)
 Call ID: 3be0039e-4ccd-46d6-a8fe-929e4f8e9afd
  Args:
    relation: :hasMother
    target: Armande_de_Pierre_de_Bernis
    source: Bruno_dHarcourt
  AssignClass (b37a54e5-b0ec-4eee-abd3-af1e4483e63a)
 Call ID: b37a54e5-b0ec-4eee-abd3-af1e4483e63a
  Args:
    type: :Man
    source: Pierre_Murat
  AssignClass (758fa0cf-5b97-4c62-8d12-bc51f309ddc2)
 Call ID: 758fa0cf-5b97-4c62-8d12-bc51f309ddc2
  Args:
    type: :Person
    source: Pierre_Murat
  AddLiteral (f22ecb35-57b0-4363-93a7-0e6d289ce4a8)
 Call ID: f22ecb35-57b0-4363-93a7-0e6d289ce4a8
  Args:
    literal_type: xsd:integer
    source: Pierre_Murat
    literal_value: 1900
    relation: :hasBirthYear
  AddLiteral (706048cf-2004-4764-90da-8af7dfc057b9)
 Call ID: 706048cf-2004-4764-90da-8af7dfc057b9
  Args:
    relation: :hasDeathYear
    literal_value: 1948
    source: Pierre_Murat
    literal_type: xsd:integer
  AddLiteral (86a4becd-95e6-4ab6-9eef-849aea6bf829)
 Call ID: 86a4becd-95e6-4ab6-9eef-849aea6bf829
  Args:
    literal_value: 1934
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Isabelle_dOrleans
  AddTriple (c897878f-d22e-4ab6-ae75-bc7e84ea7be7)
 Call ID: c897878f-d22e-4ab6-ae75-bc7e84ea7be7
  Args:
    source: Isabelle_dOrleans
    relation: :hasRelation
    target: Pierre_Murat
  AssignClass (4c313882-38f0-4f62-84ed-39afe166c1ad)
 Call ID: 4c313882-38f0-4f62-84ed-39afe166c1ad
  Args:
    type: :Man
    source: Lucien_Murat
  AssignClass (e471c8a1-f6aa-460f-a3d3-640a53409756)
 Call ID: e471c8a1-f6aa-460f-a3d3-640a53409756
  Args:
    type: :Person
    source: Lucien_Murat
  AssignClass (a585b848-eef6-489d-8809-4932bac6face)
 Call ID: a585b848-eef6-489d-8809-4932bac6face
  Args:
    type: :Woman
    source: Francoise_of_Greece
  AssignClass (955fc6c1-cd8a-46a2-9bcc-29ee59d678b8)
 Call ID: 955fc6c1-cd8a-46a2-9bcc-29ee59d678b8
  Args:
    type: :Person
    source: Francoise_of_Greece
  AddTriple (a0a15585-c01e-454d-933e-99d22c5cb89a)
 Call ID: a0a15585-c01e-454d-933e-99d22c5cb89a
  Args:
    target: Isabelle_dOrleans
    relation: :isSisterOf
    source: Francoise_of_Greece
  AssignClass (60c62d4a-eb25-40c0-a7b0-d926a734756e)
 Call ID: 60c62d4a-eb25-40c0-a7b0-d926a734756e
  Args:
    type: :Man
    source: Christopher_of_Greece
  AssignClass (0d9b2b5b-cc2c-4425-948e-9521907b6d4d)
 Call ID: 0d9b2b5b-cc2c-4425-948e-9521907b6d4d
  Args:
    type: :Person
    source: Christopher_of_Greece
  AddTriple (465e0240-8d5a-4bfd-9afb-7fd5d9a04409)
 Call ID: 465e0240-8d5a-4bfd-9afb-7fd5d9a04409
  Args:
    source: Francoise_of_Greece
    relation: :hasRelation
    target: Christopher_of_Greece
  AssignClass (2ed4a762-f8d1-41ff-a75e-22269c7a05cc)
 Call ID: 2ed4a762-f8d1-41ff-a75e-22269c7a05cc
  Args:
    type: :Man
    source: Henri_Count_of_Paris
  AssignClass (f34aa005-41f8-4daf-ada6-f6ec5f9f48c9)
 Call ID: f34aa005-41f8-4daf-ada6-f6ec5f9f48c9
  Args:
    type: :Person
    source: Henri_Count_of_Paris
  AddTriple (c416ac4c-b5b0-417c-b8f2-90f6cd373456)
 Call ID: c416ac4c-b5b0-417c-b8f2-90f6cd373456
  Args:
    relation: :isBrotherOf
    target: Isabelle_dOrleans
    source: Henri_Count_of_Paris
  AssignClass (5f97dc87-be71-411f-a35e-77dc8cb7af6c)
 Call ID: 5f97dc87-be71-411f-a35e-77dc8cb7af6c
  Args:
    type: :Man
    source: Michel_dOrleans
  AssignClass (815365ab-877e-4770-97a1-0ef2ed5a192f)
 Call ID: 815365ab-877e-4770-97a1-0ef2ed5a192f
  Args:
    type: :Person
    source: Michel_dOrleans
  AddTriple (0129124c-34d2-4a62-86d1-180703b9ce6a)
 Call ID: 0129124c-34d2-4a62-86d1-180703b9ce6a
  Args:
    source: Michel_dOrleans
    target: Henri_Count_of_Paris
    relation: :hasFather
  Finish (ffcd6e6e-1f98-4f9e-b1f7-cdfc98d663ce)
 Call ID: ffcd6e6e-1f98-4f9e-b1f7-cdfc98d663ce
  Args: