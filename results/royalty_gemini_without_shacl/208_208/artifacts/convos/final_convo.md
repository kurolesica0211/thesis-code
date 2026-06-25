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
  AssignClass (fe651143-fd07-440f-ac37-e47c39f5eee6)
 Call ID: fe651143-fd07-440f-ac37-e47c39f5eee6
  Args:
    type: :Woman
    source: Isabelle_dOrleans
  AssignClass (b663bc9b-a1c9-4c27-b701-e072f7556da9)
 Call ID: b663bc9b-a1c9-4c27-b701-e072f7556da9
  Args:
    source: Isabelle_dOrleans
    type: :Person
  AddLiteral (ac0c4031-9295-4e10-b2c3-ad8015304901)
 Call ID: ac0c4031-9295-4e10-b2c3-ad8015304901
  Args:
    literal_value: 1900
    literal_type: xsd:integer
    source: Isabelle_dOrleans
    relation: :hasBirthYear
  AddLiteral (b26fe37a-fed3-4308-802b-3e0a5cc6c17a)
 Call ID: b26fe37a-fed3-4308-802b-3e0a5cc6c17a
  Args:
    source: Isabelle_dOrleans
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1983
  AssignClass (649ad225-31ce-47fb-b8b9-0f35204a4642)
 Call ID: 649ad225-31ce-47fb-b8b9-0f35204a4642
  Args:
    source: Jean_Duke_of_Guise
    type: :Man
  AssignClass (5b40fef8-4bd0-4885-b65e-fdcec06bc176)
 Call ID: 5b40fef8-4bd0-4885-b65e-fdcec06bc176
  Args:
    type: :Person
    source: Jean_Duke_of_Guise
  AddLiteral (13fb8cc0-0ccb-417b-b699-877cfd0688ba)
 Call ID: 13fb8cc0-0ccb-417b-b699-877cfd0688ba
  Args:
    relation: :hasBirthYear
    source: Jean_Duke_of_Guise
    literal_type: xsd:integer
    literal_value: 1874
  AddLiteral (316c7410-b64f-4a55-af63-34259481fbf0)
 Call ID: 316c7410-b64f-4a55-af63-34259481fbf0
  Args:
    literal_value: 1940
    literal_type: xsd:integer
    source: Jean_Duke_of_Guise
    relation: :hasDeathYear
  AssignClass (32d45dcb-4439-4a83-b0fc-ad43827ded7f)
 Call ID: 32d45dcb-4439-4a83-b0fc-ad43827ded7f
  Args:
    source: Isabelle_of_Orleans_mother
    type: :Woman
  AssignClass (517b3aa3-53d5-42ea-b05f-c3a3268c25be)
 Call ID: 517b3aa3-53d5-42ea-b05f-c3a3268c25be
  Args:
    source: Isabelle_of_Orleans_mother
    type: :Person
  AddTriple (a66c9acc-3f30-4281-a250-9f04120d727b)
 Call ID: a66c9acc-3f30-4281-a250-9f04120d727b
  Args:
    relation: :hasFather
    source: Isabelle_dOrleans
    target: Jean_Duke_of_Guise
  AddTriple (c48c4deb-9525-4069-84bd-18fd5b3f2162)
 Call ID: c48c4deb-9525-4069-84bd-18fd5b3f2162
  Args:
    source: Isabelle_dOrleans
    relation: :hasMother
    target: Isabelle_of_Orleans_mother
  AssignClass (045996a4-33b3-4789-b79a-d014ada97e64)
 Call ID: 045996a4-33b3-4789-b79a-d014ada97e64
  Args:
    source: Bruno_dHarcourt
    type: :Man
  AssignClass (e1cdb58d-6314-43db-afb4-d079cbd155e7)
 Call ID: e1cdb58d-6314-43db-afb4-d079cbd155e7
  Args:
    type: :Person
    source: Bruno_dHarcourt
  AddLiteral (fe852667-5cf1-459e-80ff-f650d77bf0ce)
 Call ID: fe852667-5cf1-459e-80ff-f650d77bf0ce
  Args:
    literal_type: xsd:integer
    literal_value: 1899
    relation: :hasBirthYear
    source: Bruno_dHarcourt
  AddLiteral (02d5728b-2ea8-4881-adf0-2a8fb685e517)
 Call ID: 02d5728b-2ea8-4881-adf0-2a8fb685e517
  Args:
    source: Bruno_dHarcourt
    relation: :hasDeathYear
    literal_value: 1930
    literal_type: xsd:integer
  AddLiteral (3b288a18-22d5-49f1-9d1f-e11729a2ed9c)
 Call ID: 3b288a18-22d5-49f1-9d1f-e11729a2ed9c
  Args:
    relation: :hasMarriageYear
    source: Isabelle_dOrleans
    literal_value: 1923
    literal_type: xsd:integer
  AddTriple (cdae1cc1-3674-4c26-a974-68a0f1f39d48)
 Call ID: cdae1cc1-3674-4c26-a974-68a0f1f39d48
  Args:
    target: Bruno_dHarcourt
    source: Isabelle_dOrleans
    relation: :hasRelation
  AssignClass (2a696126-7765-4dcf-907c-8b92a88c9492)
 Call ID: 2a696126-7765-4dcf-907c-8b92a88c9492
  Args:
    type: :Man
    source: Eugene_dHarcourt
  AssignClass (a77009aa-5c2f-4b15-b4e0-10c4288e0176)
 Call ID: a77009aa-5c2f-4b15-b4e0-10c4288e0176
  Args:
    source: Eugene_dHarcourt
    type: :Person
  AssignClass (285d0abf-d19a-4afb-a139-16ec7ffdb641)
 Call ID: 285d0abf-d19a-4afb-a139-16ec7ffdb641
  Args:
    source: Armande_de_Pierre_de_Bernis
    type: :Woman
  AssignClass (5cfc6598-d3b5-434f-80ef-70eb2e5b8943)
 Call ID: 5cfc6598-d3b5-434f-80ef-70eb2e5b8943
  Args:
    type: :Person
    source: Armande_de_Pierre_de_Bernis
  AddTriple (7dcaf542-499b-4956-8c21-c0424cd000f2)
 Call ID: 7dcaf542-499b-4956-8c21-c0424cd000f2
  Args:
    source: Bruno_dHarcourt
    relation: :hasFather
    target: Eugene_dHarcourt
  AddTriple (62845313-bdd6-41b2-b364-20bb6a3255f0)
 Call ID: 62845313-bdd6-41b2-b364-20bb6a3255f0
  Args:
    target: Armande_de_Pierre_de_Bernis
    source: Bruno_dHarcourt
    relation: :hasMother
  AssignClass (02bdfebd-94d1-41cf-954f-409d49e8cfb8)
 Call ID: 02bdfebd-94d1-41cf-954f-409d49e8cfb8
  Args:
    type: :Man
    source: Pierre_Murat
  AssignClass (5d6ee11d-ce81-4b02-8732-b4e1d1a1466a)
 Call ID: 5d6ee11d-ce81-4b02-8732-b4e1d1a1466a
  Args:
    source: Pierre_Murat
    type: :Person
  AddLiteral (97f2cbe5-17ea-47ba-b7d5-e5b01c1b8c64)
 Call ID: 97f2cbe5-17ea-47ba-b7d5-e5b01c1b8c64
  Args:
    relation: :hasBirthYear
    source: Pierre_Murat
    literal_value: 1900
    literal_type: xsd:integer
  AddLiteral (b58f6def-a650-4425-8fd0-b7bca70e73d6)
 Call ID: b58f6def-a650-4425-8fd0-b7bca70e73d6
  Args:
    literal_value: 1948
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Pierre_Murat
  AddLiteral (7100f848-26f9-4e4f-bd09-90f1068f3101)
 Call ID: 7100f848-26f9-4e4f-bd09-90f1068f3101
  Args:
    relation: :hasMarriageYear
    source: Isabelle_dOrleans
    literal_type: xsd:integer
    literal_value: 1934
  AddTriple (8adde685-5f88-43a9-8557-34ea8bc4b640)
 Call ID: 8adde685-5f88-43a9-8557-34ea8bc4b640
  Args:
    source: Isabelle_dOrleans
    relation: :hasRelation
    target: Pierre_Murat
  AssignClass (4fe2e8e6-8dcf-436e-9e5f-9ad915bbe50a)
 Call ID: 4fe2e8e6-8dcf-436e-9e5f-9ad915bbe50a
  Args:
    type: :Man
    source: Lucien_Murat
  AssignClass (1116d79d-4676-40fb-9c8c-b291412449b9)
 Call ID: 1116d79d-4676-40fb-9c8c-b291412449b9
  Args:
    source: Lucien_Murat
    type: :Person
  AssignClass (8881bbfb-a763-45d1-b18a-9c2261f6f022)
 Call ID: 8881bbfb-a763-45d1-b18a-9c2261f6f022
  Args:
    type: :Woman
    source: Francoise_of_Greece
  AssignClass (653dd28b-e8c3-47b8-87f1-70b937f1b73f)
 Call ID: 653dd28b-e8c3-47b8-87f1-70b937f1b73f
  Args:
    source: Francoise_of_Greece
    type: :Person
  AddTriple (69cd407c-fc8a-4471-86dc-de8c5d560319)
 Call ID: 69cd407c-fc8a-4471-86dc-de8c5d560319
  Args:
    target: Francoise_of_Greece
    source: Isabelle_dOrleans
    relation: :hasSister
  AssignClass (2829aa58-8833-4452-b771-7225c28df21c)
 Call ID: 2829aa58-8833-4452-b771-7225c28df21c
  Args:
    source: Christopher_of_Greece
    type: :Man
  AssignClass (6cf5b76d-5696-43e2-af5e-6522d8803d52)
 Call ID: 6cf5b76d-5696-43e2-af5e-6522d8803d52
  Args:
    type: :Person
    source: Christopher_of_Greece
  AssignClass (b956f5b4-d1b3-46fc-aa68-f59cf3cc7426)
 Call ID: b956f5b4-d1b3-46fc-aa68-f59cf3cc7426
  Args:
    type: :Man
    source: Henri_Count_of_Paris
  AssignClass (6303b03a-07b9-441e-a89a-4a27f37f0467)
 Call ID: 6303b03a-07b9-441e-a89a-4a27f37f0467
  Args:
    source: Henri_Count_of_Paris
    type: :Person
  AddTriple (e6b4f868-3bc4-45d9-9a8f-f2c0806fbeaa)
 Call ID: e6b4f868-3bc4-45d9-9a8f-f2c0806fbeaa
  Args:
    target: Henri_Count_of_Paris
    relation: :hasBrother
    source: Isabelle_dOrleans
  AssignClass (d02f1e4c-413c-40a6-b725-eb3932e59afd)
 Call ID: d02f1e4c-413c-40a6-b725-eb3932e59afd
  Args:
    source: Michel_dOrleans
    type: :Man
  AssignClass (7ea6bda4-f450-477e-8c53-9e6ecf4c44dc)
 Call ID: 7ea6bda4-f450-477e-8c53-9e6ecf4c44dc
  Args:
    source: Michel_dOrleans
    type: :Person
  AddTriple (da8eb18e-518c-4880-b874-a6514c373194)
 Call ID: da8eb18e-518c-4880-b874-a6514c373194
  Args:
    relation: :hasFather
    source: Michel_dOrleans
    target: Henri_Count_of_Paris
  Finish (00a65afb-36ef-4fda-b023-81a5f58cdcce)
 Call ID: 00a65afb-36ef-4fda-b023-81a5f58cdcce
  Args: