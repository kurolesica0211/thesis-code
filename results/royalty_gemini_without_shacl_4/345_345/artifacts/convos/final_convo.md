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
Frederick Francis IV (Friedrich Franz Michael; 9 April 1882 – 17 November 1945) was the last Grand Duke of Mecklenburg-Schwerin and regent of Mecklenburg-Strelitz.
Early life

Born on 9 April 1882, Duke Frederick Francis IV was the son of Frederick Francis, then the hereditary grand duke of Mecklenburg-Schwerin, and Grand Duchess Anastasia Mikhailovna of Russia.
He was born in Palermo, Sicily at Villa Belmonte where his parents were staying to alleviate the faltering health of the hereditary Grand duke.
Frederick Francis's father suffered from a weak heart, chronic asthma, and acute eczema and had to live part of the year away from Mecklenburg in a warmer climate.
Frederick Francis's mother, raised in the splendor of the Russian imperial court and the Orthodox church, never got used to the provincial austerity of the Lutheran court of Schwerin, preferring to live abroad.
Frederick Francis was one year old when he became the hereditary grand duke of Mecklenburg-Schwerin at the death of his grandfather Grand Duke Frederick Francis II on 15 April 1883.
Frederick Francis IV had an older sister, Alexandrine and a younger one, Cecilie.
Friederich Franz III spent most his time hunting, while Anastasia and the children rode or drove out, visited local people or enjoyed the beach and the surrounding forest.
Grand Duke of Mecklenburg-Schwerin

Frederick Francis IV succeeded his father as Grand Duke upon his death on 10 April 1897.
As he was a teenager, due to his minority, the grand duchy was governed by his uncle Duke Johann Albrecht as regent.
Frederick Francis's mother, Grand Duchess Anastasia preferred to remain in France while he continued the long preparation to eventually assume the throne.
In 1903, the young Grand Duke moved to Bonn, where he attended university and studied administration and law.
On 9 April 1901 Frederick Francis came of age, ending the regency and beginning his reign in Schwerin.
Marriage and issue

On 7 June 1904, Frederick Francis married Princess Alexandra of Hanover in Gmunden.
She was the second eldest daughter of Ernest Augustus, Crown Prince of Hanover, and his wife, Princess Thyra of Denmark, a daughter of King Christian IX.
They had five children:


Abdication

Following the 1918 suicide of Grand Duke Adolphus Frederick VI of Mecklenburg-Strelitz, Frederick Francis took up the regency of Strelitz.
Frederick Francis abdicated the grand ducal throne on 14 November 1918 following the German Empire's defeat in World War I; the regency over the Grand Duchy of Mecklenburg-Strelitz ended at the same time.
Frederick Francis died on 17 November 1945 in Flensburg, at the age of 63, after being arrested by No6 RAF Security section on 9 November 1945.
He was succeeded as head of the grand ducal house by his son Hereditary Grand Duke Friedrich Franz.



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
  AssignClass (c51cdfd4-4137-4784-bb88-398eb5cbf7d0)
 Call ID: c51cdfd4-4137-4784-bb88-398eb5cbf7d0
  Args:
    type: :Man
    source: Frederick_Francis_IV
  AssignClass (d5969046-670d-45b8-aa1d-70c0a0e590b1)
 Call ID: d5969046-670d-45b8-aa1d-70c0a0e590b1
  Args:
    type: :Person
    source: Frederick_Francis_IV
  AddLiteral (430ff841-ef04-4536-be1c-f8d043aa0149)
 Call ID: 430ff841-ef04-4536-be1c-f8d043aa0149
  Args:
    source: Frederick_Francis_IV
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1882
  AddLiteral (d223f7db-69a4-4fac-94e2-62b81e8d5f36)
 Call ID: d223f7db-69a4-4fac-94e2-62b81e8d5f36
  Args:
    literal_value: 1945
    relation: :hasDeathYear
    source: Frederick_Francis_IV
    literal_type: xsd:integer
  AssignClass (5945c4b9-de5b-4545-b154-7c686a7705ec)
 Call ID: 5945c4b9-de5b-4545-b154-7c686a7705ec
  Args:
    type: :Man
    source: Frederick_Francis_III
  AssignClass (663b3cc1-c60a-4411-8ede-48077448c740)
 Call ID: 663b3cc1-c60a-4411-8ede-48077448c740
  Args:
    type: :Person
    source: Frederick_Francis_III
  AddTriple (a6b1b27d-6f23-4178-95b0-b5115c998687)
 Call ID: a6b1b27d-6f23-4178-95b0-b5115c998687
  Args:
    target: Frederick_Francis_III
    source: Frederick_Francis_IV
    relation: :hasFather
  AssignClass (71807a1c-8a49-4b55-8abd-e71954c9a64a)
 Call ID: 71807a1c-8a49-4b55-8abd-e71954c9a64a
  Args:
    source: Anastasia_Mikhailovna
    type: :Woman
  AssignClass (bdf9dfb4-958d-4d14-9e26-ec632a9e0f5e)
 Call ID: bdf9dfb4-958d-4d14-9e26-ec632a9e0f5e
  Args:
    type: :Person
    source: Anastasia_Mikhailovna
  AddTriple (ae62f9cb-7693-4a9d-840a-02235c35ca71)
 Call ID: ae62f9cb-7693-4a9d-840a-02235c35ca71
  Args:
    source: Frederick_Francis_IV
    target: Anastasia_Mikhailovna
    relation: :hasMother
  AssignClass (7c855c9d-2bef-4c52-b853-01b2dc0ca4d8)
 Call ID: 7c855c9d-2bef-4c52-b853-01b2dc0ca4d8
  Args:
    type: :Man
    source: Frederick_Francis_II
  AssignClass (18975fec-27e2-4f1c-ad66-f0793a534d4a)
 Call ID: 18975fec-27e2-4f1c-ad66-f0793a534d4a
  Args:
    type: :Person
    source: Frederick_Francis_II
  AddTriple (c8b748ef-01e5-4d1c-9712-86038365b056)
 Call ID: c8b748ef-01e5-4d1c-9712-86038365b056
  Args:
    target: Frederick_Francis_II
    source: Frederick_Francis_III
    relation: :hasFather
  AssignClass (b14ab85d-2d36-487e-b74c-378400536a19)
 Call ID: b14ab85d-2d36-487e-b74c-378400536a19
  Args:
    source: Alexandrine
    type: :Woman
  AssignClass (7f404885-936c-4781-b318-de8bcfa45b47)
 Call ID: 7f404885-936c-4781-b318-de8bcfa45b47
  Args:
    source: Alexandrine
    type: :Person
  AddTriple (71ba1414-00ed-4817-96bb-9dc2f0fe691d)
 Call ID: 71ba1414-00ed-4817-96bb-9dc2f0fe691d
  Args:
    source: Frederick_Francis_IV
    target: Alexandrine
    relation: :hasSister
  AssignClass (43d0e75f-71a7-4cf2-af7e-27ab102b6713)
 Call ID: 43d0e75f-71a7-4cf2-af7e-27ab102b6713
  Args:
    type: :Woman
    source: Cecilie
  AssignClass (c092d87e-155f-4fe7-a501-cca7fc374b2c)
 Call ID: c092d87e-155f-4fe7-a501-cca7fc374b2c
  Args:
    source: Cecilie
    type: :Person
  AddTriple (2cfad7d5-e015-460c-b470-050b50c6c3ff)
 Call ID: 2cfad7d5-e015-460c-b470-050b50c6c3ff
  Args:
    relation: :hasSister
    source: Frederick_Francis_IV
    target: Cecilie
  AssignClass (2dd10c80-0e8a-45b2-870b-ad041fb5408d)
 Call ID: 2dd10c80-0e8a-45b2-870b-ad041fb5408d
  Args:
    source: Johann_Albrecht
    type: :Man
  AssignClass (aa563724-643d-459c-bc11-c26f6382914a)
 Call ID: aa563724-643d-459c-bc11-c26f6382914a
  Args:
    source: Johann_Albrecht
    type: :Person
  AddTriple (f8439405-0b50-403f-b83d-20fa6f51a4f3)
 Call ID: f8439405-0b50-403f-b83d-20fa6f51a4f3
  Args:
    source: Frederick_Francis_IV
    target: Johann_Albrecht
    relation: :hasFather
  AssignClass (1062f9fa-4bc1-4e77-8b7c-7c5c14d40b51)
 Call ID: 1062f9fa-4bc1-4e77-8b7c-7c5c14d40b51
  Args:
    source: Alexandra_of_Hanover
    type: :Woman
  AssignClass (a11d6e2d-dd70-43bc-abed-792cb9b5ef4d)
 Call ID: a11d6e2d-dd70-43bc-abed-792cb9b5ef4d
  Args:
    type: :Person
    source: Alexandra_of_Hanover
  AddLiteral (639489d2-0cce-40e4-99e6-9384852b13c5)
 Call ID: 639489d2-0cce-40e4-99e6-9384852b13c5
  Args:
    literal_type: xsd:integer
    source: Frederick_Francis_IV
    literal_value: 1904
    relation: :hasMarriageYear
  AddTriple (16fdb652-539e-44a4-804d-be0bddfd4657)
 Call ID: 16fdb652-539e-44a4-804d-be0bddfd4657
  Args:
    source: Frederick_Francis_IV
    target: Alexandra_of_Hanover
    relation: :hasRelation
  AssignClass (9378f45e-f3c4-4fe6-8668-2057b3c008a1)
 Call ID: 9378f45e-f3c4-4fe6-8668-2057b3c008a1
  Args:
    source: Ernest_Augustus
    type: :Man
  AssignClass (ce016757-989c-437b-91dd-8e9a899a74d1)
 Call ID: ce016757-989c-437b-91dd-8e9a899a74d1
  Args:
    type: :Person
    source: Ernest_Augustus
  AddTriple (96ee5d12-762f-448b-bac2-052cce5c8187)
 Call ID: 96ee5d12-762f-448b-bac2-052cce5c8187
  Args:
    source: Alexandra_of_Hanover
    target: Ernest_Augustus
    relation: :hasFather
  AssignClass (44eea27f-e33c-480e-ae14-72523e1d88c1)
 Call ID: 44eea27f-e33c-480e-ae14-72523e1d88c1
  Args:
    type: :Woman
    source: Thyra_of_Denmark
  AssignClass (6aa12fdc-c4df-46ca-aa81-92cf43ba567c)
 Call ID: 6aa12fdc-c4df-46ca-aa81-92cf43ba567c
  Args:
    type: :Person
    source: Thyra_of_Denmark
  AddTriple (e50f7039-576c-4de0-a375-3eb24fa11c40)
 Call ID: e50f7039-576c-4de0-a375-3eb24fa11c40
  Args:
    relation: :hasMother
    source: Alexandra_of_Hanover
    target: Thyra_of_Denmark
  AssignClass (f51e02cb-5e63-4dee-a87d-88e1350b421d)
 Call ID: f51e02cb-5e63-4dee-a87d-88e1350b421d
  Args:
    type: :Man
    source: Christian_IX
  AssignClass (9cdc48e7-437b-46ab-88ec-e4306df7e124)
 Call ID: 9cdc48e7-437b-46ab-88ec-e4306df7e124
  Args:
    source: Christian_IX
    type: :Person
  AddTriple (2e38727d-1100-4e36-8cd4-22a58f0cf106)
 Call ID: 2e38727d-1100-4e36-8cd4-22a58f0cf106
  Args:
    target: Christian_IX
    source: Thyra_of_Denmark
    relation: :hasFather
  AssignClass (4e1d69f3-e33a-43b8-b135-0a2ae3959005)
 Call ID: 4e1d69f3-e33a-43b8-b135-0a2ae3959005
  Args:
    source: Friedrich_Franz
    type: :Man
  AssignClass (b9c81af2-3de1-49e8-a505-2ecaccb8b9c3)
 Call ID: b9c81af2-3de1-49e8-a505-2ecaccb8b9c3
  Args:
    source: Friedrich_Franz
    type: :Person
  AddTriple (53e51704-6aaf-46e4-a525-cc8898143c54)
 Call ID: 53e51704-6aaf-46e4-a525-cc8898143c54
  Args:
    relation: :hasSon
    target: Friedrich_Franz
    source: Frederick_Francis_IV
  Finish (1842f53a-c293-4188-bbd1-1535bcfb4d68)
 Call ID: 1842f53a-c293-4188-bbd1-1535bcfb4d68
  Args: