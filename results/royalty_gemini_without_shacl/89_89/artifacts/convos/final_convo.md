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
Prince Nicholas of Greece and Denmark (Greek: Νικόλαος, romanized: Nikólaos; 22 January 1872 – 8 February 1938) was the fourth child and third son of King George I of Greece, and of Queen Olga.
He was known as "Greek Nicky" within the family to distinguish him from his cousin Emperor Nicholas II of Russia (first cousin on the paternal side and second cousin on the maternal side).
Prince Nicholas was a talented painter, often signing his works as "Nicolas Leprince".
Marriage and issue

He married Grand Duchess Elena Vladimirovna of Russia (1882–1957), daughter of Grand Duke Vladimir Alexandrovich of Russia and Marie of Mecklenburg-Schwerin, the only sister of the future Russian imperial pretender, Grand Duke Kirill Vladimirovich, and his second cousin through his mother Olga Constantinovna of Russia and her father Grand Duke Vladimir Alexandrovich of Russia, on 29 August 1902 in Tsarskoye Selo, Russia.
Residence in Athens

Nicholas' marriage significantly improved his own financial position; his wife Elena received the customary imperial dowry of a Russian Grand Duchess, amounting to 1,000,000 roubles.
The dowry capital was held in Russia, from which Elena was paid an annual income of 50,000 roubles.
After their marriage the couple resided in Athens; in late 1902 they purchased a large house near the city centre, which was thereafter known as the Nicholas Palace.
Prince and Princess Nicholas took up residence at the newly-renovated Nicholas Palace in 1904.
The advent of the Russian Revolution in 1917 and the exile of the Greek Royal Family in 1923 had a significant impact on the couple's income, and as a result the Nicholas Palace was leased to the Hotel Grande Bretagne during the 1920s, who used the building as a 60-bed luxury annex known as the “Petit Palais”.
The Italian Government later purchased the Nicholas Palace from the widowed Princess Nicholas in 1955; the site has subsequently remained the home of the Italian Embassy in Athens ever since.
Public life

Along with his elder brothers Constantine and George, Nicholas helped to organize the 1896 Summer Olympics in Athens, the first to be held since 393.
Nicholas served as president of the Sub-Committee for Shooting.
His father bequeathed him the Royal Theater of Greece which Nicholas, in turn, transferred to the Greek state in 1935.
He was friends with George Simitis and was godfather to his son, future socialist Prime Minister Kostas Simitis.
Death and burial

Prince Nicholas died in Athens on February 8, 1938 and was buried in the Royal tomb at the Palace of Tatoi.



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
  AssignClass (e57d22e9-8637-439d-af23-09b433e26c7b)
 Call ID: e57d22e9-8637-439d-af23-09b433e26c7b
  Args:
    type: :Man
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (81e962de-b98d-4c1d-9e72-9de52bd59a33)
 Call ID: 81e962de-b98d-4c1d-9e72-9de52bd59a33
  Args:
    type: :Person
    source: Prince_Nicholas_of_Greece_and_Denmark
  AddLiteral (71b66b67-5238-4515-96b2-ace1a2a95ebb)
 Call ID: 71b66b67-5238-4515-96b2-ace1a2a95ebb
  Args:
    relation: :hasBirthYear
    literal_value: 1872
    literal_type: xsd:integer
    source: Prince_Nicholas_of_Greece_and_Denmark
  AddLiteral (036dc22a-dbe6-4784-9851-ebd6cf8fd0cb)
 Call ID: 036dc22a-dbe6-4784-9851-ebd6cf8fd0cb
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1938
    source: Prince_Nicholas_of_Greece_and_Denmark
  AddLiteral (c9984701-ae58-4916-830c-e2b7a4def883)
 Call ID: c9984701-ae58-4916-830c-e2b7a4def883
  Args:
    relation: :knownAs
    literal_type: xsd:string
    literal_value: Greek Nicky
    source: Prince_Nicholas_of_Greece_and_Denmark
  AddLiteral (d45fb90b-0ead-44ed-be49-55f4bbca66ee)
 Call ID: d45fb90b-0ead-44ed-be49-55f4bbca66ee
  Args:
    literal_type: xsd:string
    literal_value: Nicolas Leprince
    relation: :alsoKnownAs
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (f966bc0c-7c89-4607-8bbb-71c12bc7e7c4)
 Call ID: f966bc0c-7c89-4607-8bbb-71c12bc7e7c4
  Args:
    type: :Man
    source: King_George_I_of_Greece
  AssignClass (e7cd909d-8f30-4d16-9de7-975c768b0aa4)
 Call ID: e7cd909d-8f30-4d16-9de7-975c768b0aa4
  Args:
    type: :Person
    source: King_George_I_of_Greece
  AssignClass (6f89b88d-0b98-4ba5-81b8-f49e79cfc47a)
 Call ID: 6f89b88d-0b98-4ba5-81b8-f49e79cfc47a
  Args:
    source: Queen_Olga
    type: :Woman
  AssignClass (d6116ee0-c050-47ef-91d5-7895661dca5c)
 Call ID: d6116ee0-c050-47ef-91d5-7895661dca5c
  Args:
    type: :Person
    source: Queen_Olga
  AddTriple (5913e0e7-6afc-4069-922d-c79b746f409c)
 Call ID: 5913e0e7-6afc-4069-922d-c79b746f409c
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    relation: :hasFather
    target: King_George_I_of_Greece
  AddTriple (29398070-95ff-44a6-be9b-f28b20753547)
 Call ID: 29398070-95ff-44a6-be9b-f28b20753547
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    relation: :hasMother
    target: Queen_Olga
  AssignClass (70000330-0257-421d-bbcb-cf16487a1e42)
 Call ID: 70000330-0257-421d-bbcb-cf16487a1e42
  Args:
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    type: :Woman
  AssignClass (fb7ea1ef-5dae-4ba4-8c3b-c88390dfbbbb)
 Call ID: fb7ea1ef-5dae-4ba4-8c3b-c88390dfbbbb
  Args:
    type: :Person
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AddLiteral (7ec58805-befe-455c-88eb-25400da2c454)
 Call ID: 7ec58805-befe-455c-88eb-25400da2c454
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1902
  AddTriple (76a1174a-5013-492f-ace4-8c3ab320e18a)
 Call ID: 76a1174a-5013-492f-ace4-8c3ab320e18a
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    relation: :hasRelation
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AssignClass (2ba5def6-feb1-4802-8af0-6f37f7025481)
 Call ID: 2ba5def6-feb1-4802-8af0-6f37f7025481
  Args:
    source: Grand_Duke_Vladimir_Alexandrovich_of_Russia
    type: :Man
  AssignClass (8999ba53-b976-415b-8058-1dc13392d198)
 Call ID: 8999ba53-b976-415b-8058-1dc13392d198
  Args:
    type: :Person
    source: Grand_Duke_Vladimir_Alexandrovich_of_Russia
  AssignClass (e2eb6ed6-3dfd-45d9-a7d7-f2a1d630f1e8)
 Call ID: e2eb6ed6-3dfd-45d9-a7d7-f2a1d630f1e8
  Args:
    source: Marie_of_Mecklenburg-Schwerin
    type: :Woman
  AssignClass (406eca21-deb3-4120-ad0e-3c9ab3274a50)
 Call ID: 406eca21-deb3-4120-ad0e-3c9ab3274a50
  Args:
    type: :Person
    source: Marie_of_Mecklenburg-Schwerin
  AddTriple (6d27007f-8339-4387-97a4-ccfb9ba0368b)
 Call ID: 6d27007f-8339-4387-97a4-ccfb9ba0368b
  Args:
    relation: :hasFather
    target: Grand_Duke_Vladimir_Alexandrovich_of_Russia
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AddTriple (f073fd12-20af-43c9-b9e7-319142b9d269)
 Call ID: f073fd12-20af-43c9-b9e7-319142b9d269
  Args:
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :hasMother
    target: Marie_of_Mecklenburg-Schwerin
  AssignClass (2851890f-f42b-4abf-93d3-15243f0ce0e4)
 Call ID: 2851890f-f42b-4abf-93d3-15243f0ce0e4
  Args:
    type: :Man
    source: Grand_Duke_Kirill_Vladimirovich
  AssignClass (4e51c8af-8ed5-43cf-9674-bca817916584)
 Call ID: 4e51c8af-8ed5-43cf-9674-bca817916584
  Args:
    source: Grand_Duke_Kirill_Vladimirovich
    type: :Person
  AddTriple (c14cff34-998a-4dea-a2b8-4e43e07b4bb5)
 Call ID: c14cff34-998a-4dea-a2b8-4e43e07b4bb5
  Args:
    source: Grand_Duke_Kirill_Vladimirovich
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :hasSister
  AssignClass (55e4b6b7-aef5-476d-acaa-6dcafe05b4c1)
 Call ID: 55e4b6b7-aef5-476d-acaa-6dcafe05b4c1
  Args:
    type: :Man
    source: Constantine_of_Greece
  AssignClass (44038006-db3c-4db1-96f6-e688a147f2c1)
 Call ID: 44038006-db3c-4db1-96f6-e688a147f2c1
  Args:
    type: :Person
    source: Constantine_of_Greece
  AddTriple (f3ea788a-ff92-4ca2-a3e1-557ac436a5e0)
 Call ID: f3ea788a-ff92-4ca2-a3e1-557ac436a5e0
  Args:
    target: Constantine_of_Greece
    relation: :hasBrother
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (ff3febb7-189d-4fac-ab34-cdec454cb003)
 Call ID: ff3febb7-189d-4fac-ab34-cdec454cb003
  Args:
    source: George_of_Greece
    type: :Man
  AssignClass (8112f52f-416a-4ceb-ae79-1924bf4ce092)
 Call ID: 8112f52f-416a-4ceb-ae79-1924bf4ce092
  Args:
    source: George_of_Greece
    type: :Person
  AddTriple (0310b9b3-c4fc-4a9d-9cc6-81dadff76c39)
 Call ID: 0310b9b3-c4fc-4a9d-9cc6-81dadff76c39
  Args:
    target: George_of_Greece
    relation: :hasBrother
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (aa9947e6-3eda-46d2-940a-939f886e924e)
 Call ID: aa9947e6-3eda-46d2-940a-939f886e924e
  Args:
    type: :Man
    source: George_Simitis
  AssignClass (7b542be0-03ae-4715-96f4-a84adbad5f8a)
 Call ID: 7b542be0-03ae-4715-96f4-a84adbad5f8a
  Args:
    type: :Person
    source: George_Simitis
  AssignClass (77f0fa3f-e69c-4875-80f8-7537cba88284)
 Call ID: 77f0fa3f-e69c-4875-80f8-7537cba88284
  Args:
    source: Kostas_Simitis
    type: :Man
  AssignClass (0b8dff45-0f48-46a5-8a09-cbf2f8f6792d)
 Call ID: 0b8dff45-0f48-46a5-8a09-cbf2f8f6792d
  Args:
    source: Kostas_Simitis
    type: :Person
  AddTriple (f7f61c81-98e1-490a-bbee-8dcfe676e9bf)
 Call ID: f7f61c81-98e1-490a-bbee-8dcfe676e9bf
  Args:
    relation: :hasFather
    target: George_Simitis
    source: Kostas_Simitis
  Finish (b2437fb4-04c6-447d-ab9e-5850f8f439c7)
 Call ID: b2437fb4-04c6-447d-ab9e-5850f8f439c7
  Args: