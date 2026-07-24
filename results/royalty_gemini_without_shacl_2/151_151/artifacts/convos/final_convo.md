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
Prince Aschwin of Lippe-Biesterfeld (13 June 1914 – 14 May 1988) was an expert in Chinese painting and Indian sculpture and curator at the Metropolitan Museum of Art in New York.
He was the younger brother of Prince Bernhard of Lippe-Biesterfeld.
Life and career

Aschwin was the second and last child of Prince Bernhard of Lippe and Baroness Armgard of Sierstorpff-Cramm.
He was born with the title of count of Biesterfeld and grew up with his elder brother Bernhard at their parents' estate, Castle Reckenwalde (now Wojnowo, Lubusz Voivodeship, Poland).
When Adolf Hitler came to power, Aschwin openly supported the Nazis and became a Wehrmacht officer.
During the war, Aschwin continued his education in East Asian art.
On 11 September 1951, Prince Aschwin married Simone Arnoux (1915-2001) in London.
She was previously married to German aristocrat Gottfried Adam Vollrat von Watzdorf, from whom she had two children (Stephan von Watzdorf, born 1942, and Thilo von Watzdorf, born 1944), but none with Prince Aschwin.
After the birth of Prince Constantijn of the Netherlands on 11 October 1969, Prince Aschwin became one of his godfathers.
Although Bernhard cut off communications with Nazi supporters, including his brother, their relationships resumed after the war.
In the 1970s, Bernhard persuaded Aschwin, who was suffering from Parkinson's disease, to return to the Netherlands, where he died in 1988, aged 73.
}} Media related to Aschwin of Lippe-Biesterfeld at Wikimedia Commons



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
  AssignClass (ab930a17-6852-4604-ba75-4a7e5aedb042)
 Call ID: ab930a17-6852-4604-ba75-4a7e5aedb042
  Args:
    source: Aschwin_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (233ca876-cb41-4783-b55f-f0c546ea10b8)
 Call ID: 233ca876-cb41-4783-b55f-f0c546ea10b8
  Args:
    type: :Person
    source: Aschwin_of_Lippe-Biesterfeld
  AddLiteral (69c38638-0514-4246-80a6-b2277e60c1fc)
 Call ID: 69c38638-0514-4246-80a6-b2277e60c1fc
  Args:
    literal_type: xsd:integer
    literal_value: 1914
    source: Aschwin_of_Lippe-Biesterfeld
    relation: :hasBirthYear
  AddLiteral (d3b8aec8-48bc-4eee-af2a-34e3162e7a9a)
 Call ID: d3b8aec8-48bc-4eee-af2a-34e3162e7a9a
  Args:
    source: Aschwin_of_Lippe-Biesterfeld
    literal_value: 1988
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (ab213a81-ddc9-42ac-9a03-a564262e2fd5)
 Call ID: ab213a81-ddc9-42ac-9a03-a564262e2fd5
  Args:
    type: :Man
    source: Bernhard_of_Lippe-Biesterfeld
  AssignClass (a7010dc3-6c5d-4586-9857-16db37ae622a)
 Call ID: a7010dc3-6c5d-4586-9857-16db37ae622a
  Args:
    source: Bernhard_of_Lippe-Biesterfeld
    type: :Person
  AddTriple (9534dfca-a5c9-4f12-a3a0-0c843ede6301)
 Call ID: 9534dfca-a5c9-4f12-a3a0-0c843ede6301
  Args:
    target: Bernhard_of_Lippe-Biesterfeld
    relation: :isBrotherOf
    source: Aschwin_of_Lippe-Biesterfeld
  AssignClass (0e75f6c6-3171-44d9-ba67-9f82e0e1fcee)
 Call ID: 0e75f6c6-3171-44d9-ba67-9f82e0e1fcee
  Args:
    type: :Man
    source: Bernhard_of_Lippe
  AssignClass (0d01110a-4cdf-4d36-ac56-2d20e76c16ad)
 Call ID: 0d01110a-4cdf-4d36-ac56-2d20e76c16ad
  Args:
    type: :Person
    source: Bernhard_of_Lippe
  AssignClass (8dc7e309-c262-4c7f-a308-a67ae5904e32)
 Call ID: 8dc7e309-c262-4c7f-a308-a67ae5904e32
  Args:
    source: Armgard_of_Sierstorpff-Cramm
    type: :Woman
  AssignClass (77b79cdd-062d-447a-ae59-cd2df9876c60)
 Call ID: 77b79cdd-062d-447a-ae59-cd2df9876c60
  Args:
    source: Armgard_of_Sierstorpff-Cramm
    type: :Person
  AddTriple (a70357f0-4845-49f3-afe8-68382ff83455)
 Call ID: a70357f0-4845-49f3-afe8-68382ff83455
  Args:
    source: Aschwin_of_Lippe-Biesterfeld
    relation: :hasFather
    target: Bernhard_of_Lippe
  AddTriple (c600a6a3-c86a-42cb-b1de-fd7f0639ce48)
 Call ID: c600a6a3-c86a-42cb-b1de-fd7f0639ce48
  Args:
    relation: :hasMother
    source: Aschwin_of_Lippe-Biesterfeld
    target: Armgard_of_Sierstorpff-Cramm
  AddTriple (121c08b3-37c2-45cf-8379-3f665e5f9b29)
 Call ID: 121c08b3-37c2-45cf-8379-3f665e5f9b29
  Args:
    source: Bernhard_of_Lippe-Biesterfeld
    relation: :hasFather
    target: Bernhard_of_Lippe
  AddTriple (38ec8b46-a42c-4a36-b1b1-28f0ef4d40f2)
 Call ID: 38ec8b46-a42c-4a36-b1b1-28f0ef4d40f2
  Args:
    target: Armgard_of_Sierstorpff-Cramm
    relation: :hasMother
    source: Bernhard_of_Lippe-Biesterfeld
  AssignClass (95f41f1e-e4c4-40f7-8d24-9b28af370ca3)
 Call ID: 95f41f1e-e4c4-40f7-8d24-9b28af370ca3
  Args:
    source: Simone_Arnoux
    type: :Woman
  AssignClass (2b583328-cc4c-4fcb-9ea0-5fe66462b7d2)
 Call ID: 2b583328-cc4c-4fcb-9ea0-5fe66462b7d2
  Args:
    source: Simone_Arnoux
    type: :Person
  AddLiteral (d46e6927-f5ca-467e-9a04-e897f0dcd157)
 Call ID: d46e6927-f5ca-467e-9a04-e897f0dcd157
  Args:
    literal_type: xsd:integer
    literal_value: 1951
    source: Aschwin_of_Lippe-Biesterfeld
    relation: :hasMarriageYear
  AddTriple (03e8cdfc-4923-4a20-9ca4-c03230d7351a)
 Call ID: 03e8cdfc-4923-4a20-9ca4-c03230d7351a
  Args:
    relation: :hasRelation
    source: Aschwin_of_Lippe-Biesterfeld
    target: Simone_Arnoux
  AssignClass (510b4dcf-cc92-4280-9086-b44e40a98d0a)
 Call ID: 510b4dcf-cc92-4280-9086-b44e40a98d0a
  Args:
    source: Gottfried_Adam_Vollrat_von_Watzdorf
    type: :Man
  AssignClass (28f9dd8e-69ef-473a-8403-0c4fbbb67cfe)
 Call ID: 28f9dd8e-69ef-473a-8403-0c4fbbb67cfe
  Args:
    source: Gottfried_Adam_Vollrat_von_Watzdorf
    type: :Person
  AddTriple (d68e316a-c712-405e-a5d7-3bf3ff1bd205)
 Call ID: d68e316a-c712-405e-a5d7-3bf3ff1bd205
  Args:
    source: Simone_Arnoux
    relation: :hasRelation
    target: Gottfried_Adam_Vollrat_von_Watzdorf
  AssignClass (6501af4e-95e7-4d97-bcaf-18acb59eafee)
 Call ID: 6501af4e-95e7-4d97-bcaf-18acb59eafee
  Args:
    type: :Man
    source: Stephan_von_Watzdorf
  AssignClass (5b30d272-1acf-4c2b-8fc2-b9c9f5804617)
 Call ID: 5b30d272-1acf-4c2b-8fc2-b9c9f5804617
  Args:
    source: Stephan_von_Watzdorf
    type: :Person
  AssignClass (0deb9a1c-8fc6-4bc3-a295-92dd0aa9474c)
 Call ID: 0deb9a1c-8fc6-4bc3-a295-92dd0aa9474c
  Args:
    type: :Man
    source: Thilo_von_Watzdorf
  AssignClass (e3ba21f3-5165-417f-b68a-1cbecf2136a3)
 Call ID: e3ba21f3-5165-417f-b68a-1cbecf2136a3
  Args:
    type: :Person
    source: Thilo_von_Watzdorf
  AddTriple (77bd8b58-0a8b-43b0-aca8-519b810c1a50)
 Call ID: 77bd8b58-0a8b-43b0-aca8-519b810c1a50
  Args:
    relation: :isSonOf
    source: Stephan_von_Watzdorf
    target: Simone_Arnoux
  AddTriple (6ac5b577-738b-420b-bdfe-a1ba97fac343)
 Call ID: 6ac5b577-738b-420b-bdfe-a1ba97fac343
  Args:
    target: Gottfried_Adam_Vollrat_von_Watzdorf
    source: Stephan_von_Watzdorf
    relation: :isSonOf
  AddTriple (724d412b-e83a-4e59-87ca-121260be8869)
 Call ID: 724d412b-e83a-4e59-87ca-121260be8869
  Args:
    relation: :isSonOf
    source: Thilo_von_Watzdorf
    target: Simone_Arnoux
  AddTriple (56da273e-2a86-475f-ba5c-b38915a969ce)
 Call ID: 56da273e-2a86-475f-ba5c-b38915a969ce
  Args:
    target: Gottfried_Adam_Vollrat_von_Watzdorf
    relation: :isSonOf
    source: Thilo_von_Watzdorf
  AssignClass (4a07f707-a89d-4548-ac86-f107afd74365)
 Call ID: 4a07f707-a89d-4548-ac86-f107afd74365
  Args:
    type: :Man
    source: Constantijn_of_the_Netherlands
  AssignClass (d69503f5-dbd9-4068-a7fa-dee62eb9a8b1)
 Call ID: d69503f5-dbd9-4068-a7fa-dee62eb9a8b1
  Args:
    source: Constantijn_of_the_Netherlands
    type: :Person
  Finish (a2b41080-9fb5-4508-b5d1-2c9328509b25)
 Call ID: a2b41080-9fb5-4508-b5d1-2c9328509b25
  Args: