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
Princess Irene of the Netherlands (Irene Emma Elisabeth; born 5 August 1939) is the second child of Queen Juliana of the Netherlands and Prince Bernhard.
In 1964, she converted to Catholicism and married the then-Prince Carlos Hugo of Bourbon-Parma in a Catholic ceremony in Rome, thus forfeiting her place in the royal succession.
Childhood and family

The princess was born on 5 August 1939 at Soestdijk Palace.
She has three sisters, the eldest of whom is the former queen of the Netherlands, Princess Beatrix of the Netherlands; the two younger ones are Princess Margriet and the late Princess Christina.
Because of the invasion of the Netherlands by Nazi Germany during World War II the Dutch royal family first fled to the United Kingdom.
Irene was not yet a year old when the family was forced to leave the Netherlands; she was christened in the Chapel-Royal of Buckingham Palace in London, with the wife of King George VI, Queen Elizabeth, being one of her godparents.
When the family was leaving the Netherlands, the port where they boarded the British warship was attacked by a German air raid; one of the German bombs exploded within 200 yards of the family.
Irene was placed in a gasproof carrier to protect her from chemical warfare.
Princess Juliana and her daughters again took flight when the London Blitz began, this time to exile in Ottawa, Canada, where her younger sister, Margriet, was born and where Irene attended Rockcliffe Park Public School.
As a teenager, she was dubbed by the Dutch press "the glamorous Princess of the Netherlands."
During the war, the Royal Dutch Brigade (the formation of Free Dutch soldiers that fought alongside the Allies) was named for Princess Irene.
This was continued after the war as the Regiment Prinses Irene.
Always an independent person, Irene was thrilled to receive a sports car from her father, one of the gifts he had been presented with.
Irene's happiness was short-lived; when she opened the hood of the automobile, she noticed that the vehicle only looked like a sports car but had an ordinary car's engine.
She asked her father for permission to turn the vehicle into a true racing-type auto, which Prince Bernhard refused to allow.
She was a bridesmaid at the 1962 wedding of Prince Juan Carlos of Spain and Princess Sophia of Greece and Denmark.
Princess Irene studied at the University of Utrecht, then went to Madrid to learn the Spanish language and became proficient enough to become an official interpreter.
Marriage controversy

Conversion to Catholicism

While studying Spanish in Madrid, Irene met then Prince Carlos Hugo of Bourbon-Parma, the eldest son of Carlist claimant to the Spanish throne, Xavier, Duke of Parma and Head of the House of Bourbon-Parma.
In the summer of 1963, Princess Irene secretly converted from Protestantism to Roman Catholicism.
The first time the public or the royal family knew about the conversion was when a photograph appeared on the front page of an Amsterdam newspaper showing the Princess kneeling to receive communion at a Mass in the Roman Catholic Church of the Hieronymites (Los Jerónimos) in Madrid.
Irene's conversion took place a year before her engagement announcement, but the royal family did not officially announce the news until January 1964.
When news leaked out that she was engaged to Prince Carlos Hugo (born 1930), it provoked a Protestant outcry and a constitutional crisis.
Although Dutch law did not forbid a Catholic to reign over the Netherlands, Protestant succession was traditional, born out of the 16th-century Eighty Years' War with Spain and the assassination of William of Orange by a supporter of Philip II of Spain who believed William had betrayed both the Spanish monarch and the Catholic Church.
For the second in line to the throne to not only convert to Roman Catholicism, but to marry the heir to the Carlist claim, caused shock and consternation in the Netherlands.
When Princess Irene left the Netherlands to join Prince Carlos in Paris after the announcement of their engagement, a threat was telephoned to KLM Royal Dutch Airlines by an anonymous caller saying, "you should investigate the plane".
Queen Juliana attempted to stop the marriage, first by sending a member of her staff to Madrid to persuade the Princess not to go ahead with a marriage that would be a political disaster for the monarchy in the Netherlands.
It seemed to work and the Queen went on Dutch radio to tell the citizens that Princess Irene had agreed to cancel her engagement and was returning to the Netherlands.
When the airplane arrived at Schiphol Airport, the Princess was not on it, and Queen Juliana and her husband, Prince Bernhard were supplied with a Dutch military plane to go to Spain to retrieve their daughter.
It was suggested that Princess Irene was a pawn of General Francisco Franco who tried to maximize the event to his benefit.
Prince Bernhard then traveled to Madrid to meet with his daughter and her fiancé, who both accompanied him back to the Netherlands, where an immediate meeting took place with the couple, the Queen, Prime Minister Marijnen, himself a Roman Catholic, and three top cabinet ministers.
When the meeting ended in the early hours of the morning on Sunday, 9 February 1964, Dutch radio broke its traditional Sabbath day silence to announce that Princess Irene would give up any rights of succession to the throne so she could marry Carlos Hugo.
The princess further stated that she did not want the government to create a bill which would grant official consent to her marriage.
In an attempt to gain public favour for her proposed marriage, Princess Irene publicly stated that her marriage was intended to help end religious intolerance.
Because the constitution prohibits members of the royal family from any involvement in foreign politics, Irene alienated herself from almost every Dutch citizen when a photo appeared in a Dutch paper showing her at a Carlist rally in Spain and she declared that she supported her fiancé's political goals.
The Dutch government officially announced that it had no responsibility for either the words or actions of Princess Irene in the future on 10 April 1964.
It was done in response to Irene's declaration of joining Carlos Hugo's political campaign to regain the throne of Spain on 8 April 1964.
Marriage

Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


No one from the Dutch royal family or any Dutch diplomatic representative attended the marriage of Princess Irene and Prince Carlos Hugo in the Borghese Chapel at the Basilica di Santa Maria Maggiore in Rome, Italy, on 29 April 1964.
Dutch television provided coverage of the marriage and Irene's family was among those who watched the ceremonies, although fate conspired in the form of a power failure which made them unable to see the last part of the rite.
The Dutch royal family gathered at the home of Prince Bernhard's mother, Armgard of Sierstorpff-Cramm, for the television coverage.
Princess Armgard had also converted to Roman Catholicism like her granddaughter, but decided against attending the wedding.
Irene and her mother spoke on the telephone before she left for the Basilica.
The Dutch government had also vetoed the possibility of the wedding being held in the Netherlands.
Because she had failed to obtain the approval of the States-General to marry, Irene lost her right of succession to the Dutch throne.
She agreed that she would live outside of the Netherlands.
In 1968, Princess Irene was libeled by the West German "rainbow press".
One of the publications printed a story that Irene had undergone an abortion with parental consent before she was married.
Irene's father, Prince Bernhard, took the paper to court to clear his daughter's name.
After the wedding, Irene was very active in her husband's right-wing political cause, but over time they drifted away from right-wing extremism to left-wing sympathies and became a part of the international jet-set crowd.
On 9 May 1977 Irene was expelled from Spain on the day after the death in Switzerland of her father-in-law, the Carlist claimant Xavier, Duke of Parma.
Her husband Carlos Hugo, now the new Duke of Parma, Head of the House and Carlist claimant to the throne and an opponent of King Juan Carlos I, was also barred from the country for the same reason.
Prince Carlos Hugo was allowed to return in late 1977, but Princess Irene was not permitted back in the country until April 1978.
The prince, head of the Royal House of Bourbon-Parma, became a naturalized Spanish citizen in 1979.
Her youngest sister, Princess Christina, later waived her rights to the throne when she married Jorge Guillermo, a United States citizen born in Cuba and a Roman Catholic.
Since divorce

In 1980, Irene and her children returned to live in the Netherlands, initially moving back into Soestdijk Palace.
By 1981, she and her children had moved to their own home across the street from the palace, where Irene did traditional household chores like grocery shopping.
In 1999 Princess Irene purchased a farm near Nieu-Bethesda in South Africa, turning it into a sanctuary.
In 2001, she helped establish the NatuurCollege in the Netherlands.
She is also the founder of NatureWise, an organization that brings elementary school children in the Netherlands directly in touch with nature.
The Princess is an honorary member of the Club of Budapest.
Children

Carlos Hugo and Princess Irene had four children:


Titles, styles, and honours

Titles

Her official style is Her Royal Highness Princess Irene of the Netherlands, Princess of Orange-Nassau, Princess of Lippe-Biesterfeld.
The Princess has used the following names since her divorce:


Ancestry

References

External links

@media screen{html.skin-theme-clientpref-night .mw-parser-output .sister-inline-image img{filter:invert(1)brightness(55%)contrast(250%)hue-rotate(180deg)}}@media screen and (prefers-color-scheme:dark){html.skin-theme-clientpref-os .mw-parser-output .sister-inline-image img{filter:invert(1)brightness(55%)contrast(250%)hue-rotate(180deg)}} Media related to Princess Irene of the Netherlands at Wikimedia Commons


2 also Princess of Lippe-Biesterfeld



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
  AssignClass (502f806d-2494-4785-b4de-8d4eb0923977)
 Call ID: 502f806d-2494-4785-b4de-8d4eb0923977
  Args:
    type: :Woman
    source: Princess_Irene_of_the_Netherlands
  AssignClass (27095dd9-fad2-4f32-bad3-78976759e81a)
 Call ID: 27095dd9-fad2-4f32-bad3-78976759e81a
  Args:
    source: Princess_Irene_of_the_Netherlands
    type: :Person
  AddLiteral (45d6f566-26bf-4f45-af21-d3c33723f1d4)
 Call ID: 45d6f566-26bf-4f45-af21-d3c33723f1d4
  Args:
    relation: :hasBirthYear
    source: Princess_Irene_of_the_Netherlands
    literal_value: 1939
    literal_type: xsd:integer
  AssignClass (6d7c3eed-4dcf-478d-901b-2b3354d7df18)
 Call ID: 6d7c3eed-4dcf-478d-901b-2b3354d7df18
  Args:
    type: :Woman
    source: Queen_Juliana_of_the_Netherlands
  AssignClass (1a9e5891-944c-457f-b03d-7b4a38a08748)
 Call ID: 1a9e5891-944c-457f-b03d-7b4a38a08748
  Args:
    type: :Person
    source: Queen_Juliana_of_the_Netherlands
  AssignClass (a5fbdbe1-f946-4c3c-aa21-c14e2b993630)
 Call ID: a5fbdbe1-f946-4c3c-aa21-c14e2b993630
  Args:
    source: Prince_Bernhard
    type: :Man
  AssignClass (a25545fe-cbd6-4c0e-b777-5df847eb9d48)
 Call ID: a25545fe-cbd6-4c0e-b777-5df847eb9d48
  Args:
    source: Prince_Bernhard
    type: :Person
  AddTriple (a4893f16-513a-41d9-8264-5084cfc58f38)
 Call ID: a4893f16-513a-41d9-8264-5084cfc58f38
  Args:
    relation: :hasMother
    source: Princess_Irene_of_the_Netherlands
    target: Queen_Juliana_of_the_Netherlands
  AddTriple (107c7410-39e3-4616-aec5-8e2907144b95)
 Call ID: 107c7410-39e3-4616-aec5-8e2907144b95
  Args:
    target: Prince_Bernhard
    relation: :hasFather
    source: Princess_Irene_of_the_Netherlands
  AssignClass (9f611d1d-83be-4992-b8b5-5fdd74f91fd4)
 Call ID: 9f611d1d-83be-4992-b8b5-5fdd74f91fd4
  Args:
    source: Prince_Carlos_Hugo_of_Bourbon_Parma
    type: :Man
  AssignClass (d68b8fcc-ee3b-4515-81d5-0e8cbe423c8b)
 Call ID: d68b8fcc-ee3b-4515-81d5-0e8cbe423c8b
  Args:
    type: :Person
    source: Prince_Carlos_Hugo_of_Bourbon_Parma
  AddLiteral (6b9fc945-ec2c-40bd-b613-ca0b361b150a)
 Call ID: 6b9fc945-ec2c-40bd-b613-ca0b361b150a
  Args:
    relation: :hasMarriageYear
    literal_value: 1964
    source: Princess_Irene_of_the_Netherlands
    literal_type: xsd:integer
  AddTriple (823a7938-f94f-49d7-a102-dd01e9a44670)
 Call ID: 823a7938-f94f-49d7-a102-dd01e9a44670
  Args:
    target: Prince_Carlos_Hugo_of_Bourbon_Parma
    relation: :hasRelation
    source: Princess_Irene_of_the_Netherlands
  AssignClass (f392238c-fb99-4ce2-a1df-028678a39b7b)
 Call ID: f392238c-fb99-4ce2-a1df-028678a39b7b
  Args:
    source: Princess_Beatrix_of_the_Netherlands
    type: :Woman
  AssignClass (f303fd06-384c-43ad-946a-dca71d1b5815)
 Call ID: f303fd06-384c-43ad-946a-dca71d1b5815
  Args:
    type: :Person
    source: Princess_Beatrix_of_the_Netherlands
  AssignClass (d1671c3d-512b-4ed0-8874-ed1e3bdc6c75)
 Call ID: d1671c3d-512b-4ed0-8874-ed1e3bdc6c75
  Args:
    source: Princess_Margriet
    type: :Woman
  AssignClass (6bc540c3-20f3-4104-bc07-f88d0d15012c)
 Call ID: 6bc540c3-20f3-4104-bc07-f88d0d15012c
  Args:
    source: Princess_Margriet
    type: :Person
  AssignClass (b9d0ab71-2cc3-4e7f-bfff-23b4c333b098)
 Call ID: b9d0ab71-2cc3-4e7f-bfff-23b4c333b098
  Args:
    source: Princess_Christina
    type: :Woman
  AssignClass (2b23614f-f3a4-41d0-9a8b-c34abd9f1961)
 Call ID: 2b23614f-f3a4-41d0-9a8b-c34abd9f1961
  Args:
    source: Princess_Christina
    type: :Person
  AddTriple (1a594fbe-1269-47a4-8202-dd8315f063a8)
 Call ID: 1a594fbe-1269-47a4-8202-dd8315f063a8
  Args:
    target: Princess_Beatrix_of_the_Netherlands
    source: Princess_Irene_of_the_Netherlands
    relation: :isSisterOf
  AddTriple (e9c443e6-65b9-442f-b8f6-c2c531f34a01)
 Call ID: e9c443e6-65b9-442f-b8f6-c2c531f34a01
  Args:
    source: Princess_Irene_of_the_Netherlands
    relation: :isSisterOf
    target: Princess_Margriet
  AddTriple (2dbad15c-ed07-4319-b059-35c83adc78ab)
 Call ID: 2dbad15c-ed07-4319-b059-35c83adc78ab
  Args:
    target: Princess_Christina
    relation: :isSisterOf
    source: Princess_Irene_of_the_Netherlands
  AssignClass (0428ac2b-2fd6-4091-9354-2ed89818b7a7)
 Call ID: 0428ac2b-2fd6-4091-9354-2ed89818b7a7
  Args:
    source: Xavier_Duke_of_Parma
    type: :Man
  AssignClass (14e89179-3fda-4a90-9658-f0a702472f37)
 Call ID: 14e89179-3fda-4a90-9658-f0a702472f37
  Args:
    source: Xavier_Duke_of_Parma
    type: :Person
  AddTriple (0ea1011f-eda1-4fd3-a410-fb7aa7f1d71f)
 Call ID: 0ea1011f-eda1-4fd3-a410-fb7aa7f1d71f
  Args:
    source: Prince_Carlos_Hugo_of_Bourbon_Parma
    relation: :hasFather
    target: Xavier_Duke_of_Parma
  AssignClass (c32782bb-6e59-456b-b456-e33ff858f5c7)
 Call ID: c32782bb-6e59-456b-b456-e33ff858f5c7
  Args:
    type: :Woman
    source: Princess_Armgard_of_Sierstorpff_Cramm
  AssignClass (a6044429-494e-43d7-bd6c-9b2d76f691a0)
 Call ID: a6044429-494e-43d7-bd6c-9b2d76f691a0
  Args:
    source: Princess_Armgard_of_Sierstorpff_Cramm
    type: :Person
  AddTriple (8a653a82-6c49-4282-8f42-4ddfb3749649)
 Call ID: 8a653a82-6c49-4282-8f42-4ddfb3749649
  Args:
    relation: :hasMother
    source: Prince_Bernhard
    target: Princess_Armgard_of_Sierstorpff_Cramm
  Finish (f462bfb2-309c-44e4-b38c-5432f16a58ae)
 Call ID: f462bfb2-309c-44e4-b38c-5432f16a58ae
  Args: