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
Emich Kyrill, Prince of Leiningen (German: Emich Kirill Ferdinand Hermann Fürst zu Leiningen; 18 October 1926 – 30 October 1991) was a German entrepreneur and son of Karl, Prince of Leiningen.
Early life

Emich was born at Coburg, Weimar Republic, the first child of Karl, Prince of Leiningen (1898–1946), (son of Emich, 5th Prince of Leiningen and Princess Feodore of Hohenlohe-Langenburg) and his wife, Grand Duchess Maria Kirillovna of Russia (1907–1951), (daughter of Grand Duke Kirill Vladimirovich of Russia and Princess Victoria Melita of Edinburgh).
Through his mother, he was a descendant of Queen Victoria and Tsar Alexander II.
Through his father, he was a descendant of the Vasa kings of Sweden and of both of Queen Victoria's half-siblings, Carl, Prince of Leiningen and Feodora, Princess of Hohenlohe-Langenburg.
As a result, Emich was the first descendant of all three of Princess Victoria of Saxe-Coburg-Saalfeld's children.
Marriage

Emich married on 10 August 1950 in Rastede to Duchess Eilika of Oldenburg (2 February 1928 – 26 January 2016), fourth child and second daughter of Nikolaus, Hereditary Grand Duke of Oldenburg and Princess Helena of Waldeck and Pyrmont.



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
  AssignClass (bdacbf18-44f5-4b8d-8ab6-bc026eefe74a)
 Call ID: bdacbf18-44f5-4b8d-8ab6-bc026eefe74a
  Args:
    source: EmichKyrillPrinceOfLeiningen
    type: :Man
  AssignClass (9b376192-e64e-44e0-835d-819d8900415b)
 Call ID: 9b376192-e64e-44e0-835d-819d8900415b
  Args:
    source: KarlPrinceOfLeiningen
    type: :Man
  AssignClass (59d9f774-4e6c-45ff-ad89-4a5cef597fa9)
 Call ID: 59d9f774-4e6c-45ff-ad89-4a5cef597fa9
  Args:
    source: Emich5thPrinceOfLeiningen
    type: :Man
  AssignClass (5df8b32b-6918-44b9-88bc-18bcf15318cd)
 Call ID: 5df8b32b-6918-44b9-88bc-18bcf15318cd
  Args:
    type: :Woman
    source: PrincessFeodoreOfHohenloheLangenburg
  AssignClass (66f01601-c94e-4d22-adf3-ae784acdce12)
 Call ID: 66f01601-c94e-4d22-adf3-ae784acdce12
  Args:
    type: :Woman
    source: GrandDuchessMariaKirillovnaOfRussia
  AssignClass (45c3252a-e658-4911-8c29-8dfa6b58c3d7)
 Call ID: 45c3252a-e658-4911-8c29-8dfa6b58c3d7
  Args:
    source: GrandDukeKirillVladimirovichOfRussia
    type: :Man
  AssignClass (2354cc2c-d5eb-4bc7-bff4-8b1549049340)
 Call ID: 2354cc2c-d5eb-4bc7-bff4-8b1549049340
  Args:
    type: :Woman
    source: PrincessVictoriaMelitaOfEdinburgh
  AssignClass (82375ca0-20e1-4250-8b01-8aab86794d40)
 Call ID: 82375ca0-20e1-4250-8b01-8aab86794d40
  Args:
    source: DuchessEilikaOfOldenburg
    type: :Woman
  AssignClass (16e93e13-06d2-40b2-a9e5-f7d9adc84029)
 Call ID: 16e93e13-06d2-40b2-a9e5-f7d9adc84029
  Args:
    source: NikolausHereditaryGrandDukeOfOldenburg
    type: :Man
  AssignClass (325d618c-04bd-4e20-9488-47f2149ab679)
 Call ID: 325d618c-04bd-4e20-9488-47f2149ab679
  Args:
    type: :Woman
    source: PrincessHelenaOfWaldeckAndPyrmont
  AddLiteral (b724639e-e86d-4690-b495-fc4fe1bb32a2)
 Call ID: b724639e-e86d-4690-b495-fc4fe1bb32a2
  Args:
    literal_type: xsd:integer
    literal_value: 1926
    relation: :hasBirthYear
    source: EmichKyrillPrinceOfLeiningen
  AddLiteral (051b0071-4161-44ec-b486-973ca7d7ed3a)
 Call ID: 051b0071-4161-44ec-b486-973ca7d7ed3a
  Args:
    literal_value: 1991
    literal_type: xsd:integer
    source: EmichKyrillPrinceOfLeiningen
    relation: :hasDeathYear
  AddTriple (079b51e8-dff2-48c3-b2cf-128b5ae335d2)
 Call ID: 079b51e8-dff2-48c3-b2cf-128b5ae335d2
  Args:
    relation: :hasFather
    source: EmichKyrillPrinceOfLeiningen
    target: KarlPrinceOfLeiningen
  AddTriple (1a0e47dc-693b-454a-9493-8a3b8135d878)
 Call ID: 1a0e47dc-693b-454a-9493-8a3b8135d878
  Args:
    relation: :hasMother
    source: EmichKyrillPrinceOfLeiningen
    target: GrandDuchessMariaKirillovnaOfRussia
  AddLiteral (a3f97d7f-dced-4c7d-bcd4-e9406e0dbe2e)
 Call ID: a3f97d7f-dced-4c7d-bcd4-e9406e0dbe2e
  Args:
    literal_value: 1898
    literal_type: xsd:integer
    source: KarlPrinceOfLeiningen
    relation: :hasBirthYear
  AddLiteral (2a64d1f8-b6a4-436e-867d-2984f05cd540)
 Call ID: 2a64d1f8-b6a4-436e-867d-2984f05cd540
  Args:
    relation: :hasDeathYear
    source: KarlPrinceOfLeiningen
    literal_type: xsd:integer
    literal_value: 1946
  AddTriple (8a355191-9307-4046-ae39-c0dc9cc404cb)
 Call ID: 8a355191-9307-4046-ae39-c0dc9cc404cb
  Args:
    target: Emich5thPrinceOfLeiningen
    relation: :hasFather
    source: KarlPrinceOfLeiningen
  AddTriple (5d75c269-cd2c-48eb-8a87-f33e40d3f582)
 Call ID: 5d75c269-cd2c-48eb-8a87-f33e40d3f582
  Args:
    relation: :hasMother
    source: KarlPrinceOfLeiningen
    target: PrincessFeodoreOfHohenloheLangenburg
  AddLiteral (3bd53980-0277-4cc6-9415-3cb02b858836)
 Call ID: 3bd53980-0277-4cc6-9415-3cb02b858836
  Args:
    relation: :hasBirthYear
    source: GrandDuchessMariaKirillovnaOfRussia
    literal_type: xsd:integer
    literal_value: 1907
  AddLiteral (414aa945-8e79-4f54-a42c-03664f04af3e)
 Call ID: 414aa945-8e79-4f54-a42c-03664f04af3e
  Args:
    relation: :hasDeathYear
    source: GrandDuchessMariaKirillovnaOfRussia
    literal_type: xsd:integer
    literal_value: 1951
  AddTriple (de0885ef-3e8c-4d6d-8ee4-fa92b914989c)
 Call ID: de0885ef-3e8c-4d6d-8ee4-fa92b914989c
  Args:
    source: GrandDuchessMariaKirillovnaOfRussia
    relation: :hasFather
    target: GrandDukeKirillVladimirovichOfRussia
  AddTriple (88557224-ef62-439d-929a-5b69d2ad6aa2)
 Call ID: 88557224-ef62-439d-929a-5b69d2ad6aa2
  Args:
    target: PrincessVictoriaMelitaOfEdinburgh
    relation: :hasMother
    source: GrandDuchessMariaKirillovnaOfRussia
  AddTriple (b8cfbcf1-32b0-4c28-856e-1169aa1a8e54)
 Call ID: b8cfbcf1-32b0-4c28-856e-1169aa1a8e54
  Args:
    source: EmichKyrillPrinceOfLeiningen
    relation: :hasRelation
    target: DuchessEilikaOfOldenburg
  AddLiteral (690f3062-105b-4ab9-8567-af391bf0cd8f)
 Call ID: 690f3062-105b-4ab9-8567-af391bf0cd8f
  Args:
    source: EmichKyrillPrinceOfLeiningen
    relation: :hasMarriageYear
    literal_value: 1950
    literal_type: xsd:integer
  AddLiteral (5f2ebfb8-d6ff-4875-8234-e350bed20711)
 Call ID: 5f2ebfb8-d6ff-4875-8234-e350bed20711
  Args:
    source: DuchessEilikaOfOldenburg
    relation: :hasBirthYear
    literal_value: 1928
    literal_type: xsd:integer
  AddLiteral (3689e1f5-2294-4685-9fc1-f48b96e59812)
 Call ID: 3689e1f5-2294-4685-9fc1-f48b96e59812
  Args:
    source: DuchessEilikaOfOldenburg
    relation: :hasDeathYear
    literal_value: 2016
    literal_type: xsd:integer
  AddTriple (f22d7c1e-0fe3-4425-b4ea-4be011e4dcb3)
 Call ID: f22d7c1e-0fe3-4425-b4ea-4be011e4dcb3
  Args:
    relation: :hasFather
    source: DuchessEilikaOfOldenburg
    target: NikolausHereditaryGrandDukeOfOldenburg
  AddTriple (6f050519-f394-4c89-bcb2-f959ae7eac22)
 Call ID: 6f050519-f394-4c89-bcb2-f959ae7eac22
  Args:
    relation: :hasMother
    source: DuchessEilikaOfOldenburg
    target: PrincessHelenaOfWaldeckAndPyrmont
  Finish (79c59e54-da48-44ed-88e3-38acf365216e)
 Call ID: 79c59e54-da48-44ed-88e3-38acf365216e
  Args: